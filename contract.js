pragma solidity >=0.7.0 <0.9.0;

// заполненный словарь, в котором лежит соответствие id участнику процесса
mapping(address => Participant) public participants;
// множество функций, которые возвращают, какими транспортными компаниями нужно воспользоваться,
// к какому банку обратиться, какие вокзалы-аэропорты будут задействованы и проч.
// это поход как правило будет поход в БД или в иной бэкенд, или создание запроса специалисту
function getInfo(address _to, address _from, Request request) {}
// ...

// товар
struct Product {
	uint public ProductId;
	string public Name;
	string public Measure; // единицы измерения – штуки, килограммы, банки и проч.
	// Иные параметры – штрих-коды, название на других языках, форма выпуска и проч.
}

struct Request {
	uint Id;
	address RequestAddress;
	Date RequestDate;
	Product[] Products;
	uint[] Counts; // количества каждого товара
	string Message;
	bool ErrorInModifying;
	bool Done; 
	// Иные параметры
}

struct Approve {
	uint Id;
	address ApproveAddress;
	Date ApproveDate;
	Request request;
	string Message;
}

// участник процесса, интерфейс
contract Participant {
	address public Address;
	string public Name;
	Requests[] public requests; // заявки в этот сервис
	public approves = {}; // ответы на заявки
	// всякие-разные поля типа ИНН, банковских счетов, ФИО контактного лица, email...
	[]Participant participants; // все участники
	mapping(uint => bool) public Done; // сервер выставляет в каждом участнике bool у заявки, если она успешно обработана
}

// Не покупатель. Эти участники – транспортные хабы, транспортные компании, банки, продавец – должны подтвердить участие в сделке.
// вполне вероятно, что они модифицируют request, заполняя какие-то поля
contract ApprovableParticipant is Participant {
	// функции нужны для того, чтобы компания-партнер подтвердила свою возможность и желание участвовать 
	// в нашем запросе. Первая функция отправляет заявки на бекенд, где по какой-то сложной логике она обрабатывается,
	// здесь блокчейн не нужен и это происходит где-то внутри IT-системы партнера

	// заявку обрабатывает бекенд или эксперт. Эта функция должна быть перегружена для каждого партнера.
	function getApprove(Request _request) (bool accepted) {}

	// функция approve разбирает асинхронно очередь Requests[] requests
	// не понял, как тут сделать асинхронные срабатывания с прослушиванием канала.
	// По сути, это будет что-то типа select/poll/epoll из мира операционных систем
	function approve(address _to, address _from, Request _request) (bool accepted) {
		bool ans = getApprove(Request _request);
		participants[_to].approves[hash(_to, _from, _request.id)] = ans;
	}
}

// транспортные хабы, транспортные компании, банки. Обрабатывают по одному этапу пайплайна
contract SecondaryParticipant is ApprovableParticipant {

	// перегружаемая функция, которая непосредственно выполняет часть контракта
	function transferRunPart(address _to, address _from, Request _request) constant returns (Request modified) {}
}

// Этакий сервер
contract Buyer is Participant {
	// запрос продавцу
	function transfer(address _to, address _from, Request _request) constant returns (bool accepted) {
		participants[_to].requests.push(_request);
		// здесь в цикле как-то умно ожидаем, пока придет ответ, и потом
		if (approve[hash(_to, _from, _request.id, participants[_to].Address)]) {
			participants.push(_to);

			// получаем информацию о том, какие участники нужны нужны
			// если какие-то не нужны ИЛИ мы сами уже и есть этот участник, то будет []
			// такой интерфейс нужен, чтобы не было кучи дублирования кода.


			// ЗДЕСЬ ОЧЕНЬ ВАЖНО, чтобы вернулись все партнеры в нужном порядке, то есть в порядке, 
			// в котором они будут обрабатывать заявку в нашем конвейере.
			// реализация функции getInfo живет где-то на бэкенде и при ее выполнении, 
			// возможно, потребуется вмешательство лиц, принимающих решение.
			SecondaryParticipant[] partners = getInfo(address _to, Request _request);


			// аналогично делаем transferPart - запросы в транспортные компании, банки и хабы
			for (uint i = 0; i < partners.length; i++) {
				bool ansPart = transferPart(partners[i].address, _request)
				if (!ansPart) {
					return false;
				}
				participants.push(banks[i].address);
			}

			// Запускаем на исполнение заявку
			bool res = transferRun(_to, _from, _request, participants);
			if (res) {
				_request.Done = true;
				participants[_to][_request.Id] = true; // говорим продавцу, что товар к нам пришел
			}
			return res;
		}

		// отвалились по таймауту, т.к. не пришел ответ от кого-то
		return false;
	}

	// Запускаем выполение пайплайна. Для каждого Participant определяем реализацию функции transferRun.
	// За счет полиморфизма для каждого Participant будет вызван нужный обработчик.
	function transferRun(address _to, address _from, Request _request, Participant[] participants) constant returns (bool accepted) {
		Request request = _request;
		for (uint i = 0; i < participants.length; i++) {
			// Каждая операция модифицирует запрос. Тогда каждый следующий обработчик должен работать с обновленным запросом
			request = participants[i].transferRunPart(_to, _from, request);
			if (request.ErrorInModifying) {
				return false;
			}
			participants[i][_request.Id] = true; // говорим партнеру, что он молодец
		}
		return true;
	}


	// запросы всем остальным
	function transferPart(address _to, address _from, Request _request) constant returns (bool accepted) {
		participants[_to].requests.push(_request);
		// в цикле как-то умно ожидаем, пока придет ответ, и потом
		return approves[hash(_to, _from, _request.id, participants[_to].Address)]
	}

}

// Клиенты
contract Seller is ApprovableParticipant {
	function getApprove(Request _request) (bool accepted) {
		// здесь какой-то запрос к внутренней системе партнера
	}

}


contract Bank is SecondaryParticipant {
	function getApprove(Request _request) (bool accepted) {
		// здесь какой-то запрос к внутренней системе партнера
	}

	function transferRunPart(address _to, address _from, Request _request) constant returns (Request modified) {
		// здесь какой-то запрос к внутренней системе партнера
	}
}

contract TransportCompany is SecondaryParticipant {
	function getApprove(Request _request) (bool accepted) {
		// здесь какой-то запрос к внутренней системе партнера
	}

	function transferRunPart(address _to, address _from, Request _request) constant returns (Request modified) {
		// здесь какой-то запрос к внутренней системе партнера
	}

}

contract Hub is SecondaryParticipant {
	function getApprove(Request _request) (bool accepted) {
		// здесь какой-то запрос к внутренней системе партнера
	}

	function transferRunPart(address _to, address _from, Request _request) constant returns (Request modified) {
		// здесь какой-то запрос к внутренней системе партнера
	}

}
